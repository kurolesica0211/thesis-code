================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Amedeo of Savoy-Aosta, 5th Duke of Aosta (Amedeo Umberto Costantino Giorgio
Early life

Amedeo was born at Villa della Cisterna in Florence, the only child of Prince Aimone, Duke of Aosta, formerly designated king of Croatia as Tomislav II, and of Princess Irene of Greece and Denmark through whom he was a great-great-grandson of Queen Victoria.
When Amedeo was only four years old, his father died in exile in Buenos Aires, and he succeeded him as Duke of Aosta, Prince della Cisterna e Belriguardo, Marchese di Voghera, and Count di Ponderano.
He was an Honorary Companion of the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States, assigned insignia number 21015, as a great-grandson of Prince Philippe, Count of Paris.
Marriages and family

1st marriage and descendants

On 22 July 1964, at the Igreja Paroquial De São Pedro in Sintra, Portugal, Amedeo married his second cousin, Princess Claude of Orléans (born 11 December 1943).
She was the ninth child and fifth daughter of Henri, comte de Paris, Orléanist claimant to the French throne, and of Princess Isabelle of Orléans-Braganza.
He was involved in various agricultural activities, including the production of wine marketed under the name Vini Savoia Aosta.
Dynastic activities

Amedeo was long viewed by Italian royalists as a likely claimant to the throne if Umberto's own son, Vittorio Emanuele, Prince of Naples, failed to live up to monarchist expectations.
On 7 July 2006, Amedeo declared himself to be the Head of the House of Savoy and Duke of Savoy, claiming that in 1971, Vittorio Emanuele had lost his dynastic rights when he married without previously obtaining the permission of Umberto II, authorization which had been required under monarchical law.
In 2009, Vittorio Emanuele and his son, Emanuele Filiberto, Prince of Venice, sought judicial intervention to forbid Amedeo's use of the surname di Savoia.
In February 2010, the court of Arezzo ruled that the Amedeo and his son Aimone must pay damages totalling 50,000 euros to their cousins and cease using the surname di Savoia instead of di Savoia-Aosta.
Amedeo's claim received the support of Vittorio Emanuele's sister, Princess Maria Gabriella of Savoy.
Although many monarchists transferred their allegiance to Amedeo at some point after King Umberto's death, Amedeo was criticised by other Italian royalists who continue to support Prince Vittorio Emanuele.
But others, including constitutional jurist Guido Locatello, declared the marriage of Vittorio Emanuele to be in violation of Savoy dynastic law years before the scandal evoked any clamour for Amedeo to replace him.
The Unione Monarchica Italiana published in its newsletter, Monarchia Nuova, on 12 February 1987 that the Prince of Naples' marriage to Marina Doria violated the decree of Victor Amadeus III, issued 13 September 1780, regulating the marriages of princes of the blood royal, compelling the Unione to recognise Amedeo as rightful head of the royal house—although at that time Aosta had put forth no public dynastic claim.
Amedeo was a Knight of the Supreme Order of the Most Holy Annunciation named by Umberto II, a Grand Cross of the Order of Saints Maurice and Lazarus named by his cousin Vittorio Emanuele, and a Knight of Honor and Devotion of the Sovereign Military Order of St. John of Jerusalem.
Death

Prince Amedeo died on 1 June 2021, at the age of 77, in Arezzo, Italy, from cardiac arrest after undergoing surgery on 27 May.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (2b2bda47-675c-4290-b2b2-3365d88e66e4)
 Call ID: 2b2bda47-675c-4290-b2b2-3365d88e66e4
  Args:
    type: :Man
    source: Prince_Amedeo_of_Savoy-Aosta
  AssignClass (e0a6b1e8-3e35-454a-b307-c69b82db2b5c)
 Call ID: e0a6b1e8-3e35-454a-b307-c69b82db2b5c
  Args:
    type: :Person
    source: Prince_Amedeo_of_Savoy-Aosta
  AddLiteral (67dc1f6b-6cc4-414b-812e-d4d67cc0240c)
 Call ID: 67dc1f6b-6cc4-414b-812e-d4d67cc0240c
  Args:
    literal_type: xsd:integer
    literal_value: 2021
    source: Prince_Amedeo_of_Savoy-Aosta
    relation: :hasDeathYear
  AssignClass (e99474a0-6568-4f50-9ec4-12a3c0713325)
 Call ID: e99474a0-6568-4f50-9ec4-12a3c0713325
  Args:
    type: :Man
    source: Prince_Aimone_Duke_of_Aosta
  AssignClass (cb5c71d0-791c-429a-97cd-34309613df93)
 Call ID: cb5c71d0-791c-429a-97cd-34309613df93
  Args:
    type: :Person
    source: Prince_Aimone_Duke_of_Aosta
  AddTriple (8a762cbe-6ac6-497e-a4d4-a020d1cedf22)
 Call ID: 8a762cbe-6ac6-497e-a4d4-a020d1cedf22
  Args:
    target: Prince_Aimone_Duke_of_Aosta
    source: Prince_Amedeo_of_Savoy-Aosta
    relation: :hasFather
  AssignClass (1ea970db-d88d-4bcc-9f38-492c6eafa9db)
 Call ID: 1ea970db-d88d-4bcc-9f38-492c6eafa9db
  Args:
    type: :Woman
    source: Princess_Irene_of_Greece_and_Denmark
  AssignClass (76e208ad-9a53-4145-bb32-fe4e7af102e4)
 Call ID: 76e208ad-9a53-4145-bb32-fe4e7af102e4
  Args:
    type: :Person
    source: Princess_Irene_of_Greece_and_Denmark
  AddTriple (21dcac51-6ea9-4b19-bc2c-4d8ae49f9759)
 Call ID: 21dcac51-6ea9-4b19-bc2c-4d8ae49f9759
  Args:
    relation: :hasMother
    target: Princess_Irene_of_Greece_and_Denmark
    source: Prince_Amedeo_of_Savoy-Aosta
  AssignClass (b7cb483a-aff8-4663-bbd9-bf2204a1dc41)
 Call ID: b7cb483a-aff8-4663-bbd9-bf2204a1dc41
  Args:
    type: :Woman
    source: Princess_Claude_of_Orléans
  AssignClass (5785c4e7-6dcd-4e76-b17e-fd991c70086d)
 Call ID: 5785c4e7-6dcd-4e76-b17e-fd991c70086d
  Args:
    type: :Person
    source: Princess_Claude_of_Orléans
  AddLiteral (383abb01-da3c-4130-847c-9ed41e323224)
 Call ID: 383abb01-da3c-4130-847c-9ed41e323224
  Args:
    relation: :hasMarriageYear
    literal_value: 1964
    literal_type: xsd:integer
    source: Prince_Amedeo_of_Savoy-Aosta
  AddTriple (a1191837-2744-4211-a493-49c7a2fd46a5)
 Call ID: a1191837-2744-4211-a493-49c7a2fd46a5
  Args:
    target: Princess_Claude_of_Orléans
    source: Prince_Amedeo_of_Savoy-Aosta
    relation: :hasRelation
  AssignClass (d2600359-eb06-48d4-be3a-b09766f6b8ed)
 Call ID: d2600359-eb06-48d4-be3a-b09766f6b8ed
  Args:
    type: :Man
    source: Henri_comte_de_Paris
  AssignClass (c6ea2250-7bd6-420e-810f-ab5580dc4560)
 Call ID: c6ea2250-7bd6-420e-810f-ab5580dc4560
  Args:
    type: :Person
    source: Henri_comte_de_Paris
  AddTriple (d8300eef-be72-492c-99ef-22893c477dee)
 Call ID: d8300eef-be72-492c-99ef-22893c477dee
  Args:
    relation: :hasFather
    source: Princess_Claude_of_Orléans
    target: Henri_comte_de_Paris
  AssignClass (81ff280c-11a0-44ca-90ab-ce5b728e0acc)
 Call ID: 81ff280c-11a0-44ca-90ab-ce5b728e0acc
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orléans-Braganza
  AssignClass (7c1eaa29-cb14-4022-9e0d-810d61d99bd7)
 Call ID: 7c1eaa29-cb14-4022-9e0d-810d61d99bd7
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orléans-Braganza
  AddTriple (78de2330-99b5-4b2e-9929-c8305736012c)
 Call ID: 78de2330-99b5-4b2e-9929-c8305736012c
  Args:
    relation: :hasMother
    source: Princess_Claude_of_Orléans
    target: Princess_Isabelle_of_Orléans-Braganza
  AssignClass (bddffe43-9ac1-4ef0-8a7e-8a4df9224eb3)
 Call ID: bddffe43-9ac1-4ef0-8a7e-8a4df9224eb3
  Args:
    type: :Man
    source: Aimone_son_of_Amedeo
  AssignClass (96cc500d-c753-46ea-aa80-ae44e4433a5c)
 Call ID: 96cc500d-c753-46ea-aa80-ae44e4433a5c
  Args:
    type: :Person
    source: Aimone_son_of_Amedeo
  AddTriple (bf5c72ca-6aa4-4a5b-8457-93c3c7ac764f)
 Call ID: bf5c72ca-6aa4-4a5b-8457-93c3c7ac764f
  Args:
    target: Prince_Amedeo_of_Savoy-Aosta
    source: Aimone_son_of_Amedeo
    relation: :isSonOf
  AssignClass (308a25c7-10b1-47d4-b41d-d7d7038e7d44)
 Call ID: 308a25c7-10b1-47d4-b41d-d7d7038e7d44
  Args:
    type: :Man
    source: Vittorio_Emanuele_Prince_of_Naples
  AssignClass (63d6e048-7581-404e-b426-c8bef5868296)
 Call ID: 63d6e048-7581-404e-b426-c8bef5868296
  Args:
    type: :Person
    source: Vittorio_Emanuele_Prince_of_Naples
  AssignClass (ad4bd778-dfbb-443e-9ce3-a5318748588d)
 Call ID: ad4bd778-dfbb-443e-9ce3-a5318748588d
  Args:
    type: :Man
    source: Emanuele_Filiberto_Prince_of_Venice
  AssignClass (d480d4ae-9d08-4c8c-98b6-5cb913de60ca)
 Call ID: d480d4ae-9d08-4c8c-98b6-5cb913de60ca
  Args:
    type: :Person
    source: Emanuele_Filiberto_Prince_of_Venice
  AddTriple (cc3e7c32-335a-473e-91e9-3de67aa6f8b3)
 Call ID: cc3e7c32-335a-473e-91e9-3de67aa6f8b3
  Args:
    target: Vittorio_Emanuele_Prince_of_Naples
    source: Emanuele_Filiberto_Prince_of_Venice
    relation: :isSonOf
  AssignClass (488e5cf2-bd5b-4313-b2ea-98bfe65700d2)
 Call ID: 488e5cf2-bd5b-4313-b2ea-98bfe65700d2
  Args:
    type: :Woman
    source: Princess_Maria_Gabriella_of_Savoy
  AssignClass (4dc27498-5eee-4de0-8dfc-3096c2d289ea)
 Call ID: 4dc27498-5eee-4de0-8dfc-3096c2d289ea
  Args:
    type: :Person
    source: Princess_Maria_Gabriella_of_Savoy
  AddTriple (a953499d-1ccc-47e9-8b95-b89513ce9dd1)
 Call ID: a953499d-1ccc-47e9-8b95-b89513ce9dd1
  Args:
    relation: :isSisterOf
    target: Vittorio_Emanuele_Prince_of_Naples
    source: Princess_Maria_Gabriella_of_Savoy
  Finish (94e8a845-b1ee-4697-95d3-f2fcc727320c)
 Call ID: 94e8a845-b1ee-4697-95d3-f2fcc727320c
  Args: