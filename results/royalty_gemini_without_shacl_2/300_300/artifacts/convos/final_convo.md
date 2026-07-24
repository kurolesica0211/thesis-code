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
  AssignClass (40d99baa-a286-45d1-ae3f-97dbe80c8a76)
 Call ID: 40d99baa-a286-45d1-ae3f-97dbe80c8a76
  Args:
    source: :Prince_Amedeo_of_Savoy-Aosta
    type: :Man
  AssignClass (1379af76-9013-47aa-b7e8-74d323823052)
 Call ID: 1379af76-9013-47aa-b7e8-74d323823052
  Args:
    source: :Prince_Aimone_Duke_of_Aosta
    type: :Man
  AssignClass (20e491a1-f7b3-4946-8c34-7f9770c8313f)
 Call ID: 20e491a1-f7b3-4946-8c34-7f9770c8313f
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (0821f746-124e-47d5-82ec-38d2438ae23c)
 Call ID: 0821f746-124e-47d5-82ec-38d2438ae23c
  Args:
    source: :Princess_Claude_of_Orleans
    type: :Woman
  AssignClass (c6061fac-403e-4e1b-a1b8-99393a0522ed)
 Call ID: c6061fac-403e-4e1b-a1b8-99393a0522ed
  Args:
    source: :Henri_comte_de_Paris
    type: :Man
  AssignClass (341f511c-01aa-4b4b-a33c-9e138211a076)
 Call ID: 341f511c-01aa-4b4b-a33c-9e138211a076
  Args:
    source: :Princess_Isabelle_of_Orleans-Braganza
    type: :Woman
  AssignClass (99e216ea-dab6-4ba5-99f3-684e2b023d25)
 Call ID: 99e216ea-dab6-4ba5-99f3-684e2b023d25
  Args:
    type: :Man
    source: :Vittorio_Emanuele_Prince_of_Naples
  AssignClass (8414b66d-3cd3-43be-9d06-3fa028d6c90f)
 Call ID: 8414b66d-3cd3-43be-9d06-3fa028d6c90f
  Args:
    type: :Man
    source: :Emanuele_Filiberto_Prince_of_Venice
  AssignClass (102ef11a-967b-4730-bb0e-374a0a6a3ddd)
 Call ID: 102ef11a-967b-4730-bb0e-374a0a6a3ddd
  Args:
    source: :Princess_Maria_Gabriella_of_Savoy
    type: :Woman
  AssignClass (109dba4c-e310-4b1e-8768-660c8d3ec42a)
 Call ID: 109dba4c-e310-4b1e-8768-660c8d3ec42a
  Args:
    source: :Umberto_II
    type: :Man
  AssignClass (2783c7d3-cf05-4396-a214-be44432aa380)
 Call ID: 2783c7d3-cf05-4396-a214-be44432aa380
  Args:
    type: :Man
    source: :Aimone
  AddTriple (bfe27352-f743-4031-9a77-1c4964d23d3f)
 Call ID: bfe27352-f743-4031-9a77-1c4964d23d3f
  Args:
    source: :Prince_Amedeo_of_Savoy-Aosta
    target: :Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
  AddTriple (76db0238-01ac-46f9-85c9-97bf2d03e935)
 Call ID: 76db0238-01ac-46f9-85c9-97bf2d03e935
  Args:
    relation: :hasMother
    target: :Princess_Irene_of_Greece_and_Denmark
    source: :Prince_Amedeo_of_Savoy-Aosta
  AddTriple (15d75e5e-922a-40c5-83a5-5f8d40b850d1)
 Call ID: 15d75e5e-922a-40c5-83a5-5f8d40b850d1
  Args:
    target: :Henri_comte_de_Paris
    source: :Princess_Claude_of_Orleans
    relation: :hasFather
  AddTriple (d95fd10f-d3a5-41a7-88ef-71b34c1babd3)
 Call ID: d95fd10f-d3a5-41a7-88ef-71b34c1babd3
  Args:
    relation: :hasMother
    target: :Princess_Isabelle_of_Orleans-Braganza
    source: :Princess_Claude_of_Orleans
  AddTriple (5400e37d-b75b-45f9-b49f-413cdc3ef452)
 Call ID: 5400e37d-b75b-45f9-b49f-413cdc3ef452
  Args:
    relation: :hasFather
    source: :Emanuele_Filiberto_Prince_of_Venice
    target: :Vittorio_Emanuele_Prince_of_Naples
  AddTriple (10057a2d-0169-4e2e-87e9-f03e3971b15f)
 Call ID: 10057a2d-0169-4e2e-87e9-f03e3971b15f
  Args:
    relation: :hasFather
    target: :Prince_Amedeo_of_Savoy-Aosta
    source: :Aimone
  AddLiteral (39f7831a-07c4-4ade-8c10-8c32723bef83)
 Call ID: 39f7831a-07c4-4ade-8c10-8c32723bef83
  Args:
    relation: :hasDeathYear
    literal_value: 2021
    literal_type: xsd:integer
    source: :Prince_Amedeo_of_Savoy-Aosta
  AddLiteral (213d3b42-0772-4c6f-9e4a-ea0f5b4205ec)
 Call ID: 213d3b42-0772-4c6f-9e4a-ea0f5b4205ec
  Args:
    literal_type: xsd:integer
    source: :Prince_Amedeo_of_Savoy-Aosta
    relation: :hasMarriageYear
    literal_value: 1964
  Finish (3bb4ee3a-df11-427a-bbe0-290b68a9ad14)
 Call ID: 3bb4ee3a-df11-427a-bbe0-290b68a9ad14
  Args: