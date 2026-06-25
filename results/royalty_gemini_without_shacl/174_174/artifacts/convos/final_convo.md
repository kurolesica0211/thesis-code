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
Princess Katherine of Greece and Denmark (Greek: Αικατερίνη; 4 May 1913 – 2 October 2007), styled in the United Kingdom as Lady Katherine Brandram from 1947 until 2007, was the third daughter and youngest child of King Constantine I of Greece and Princess Sophia of Prussia.
Early life

Katherine was born on 4 May 1913 in the Royal Palace in Athens, a few weeks after her paternal grandfather, King George I of Greece, was assassinated in Thessaloniki.
Her godparents were Olga Constantinovna (the Dowager Queen of Greece, her paternal grandmother), Alexandra (the Dowager Queen of the United Kingdom, her paternal grandfather's sister and her maternal grandmother's sister-in-law), George V (the King of the United Kingdom, her mother's maternal cousin and her father's paternal cousin), Wilhelm II, German Emperor (her maternal uncle), The Greek Navy (represented by the Minister of Marine) and The Greek Army (represented by the Minister of War).
Katherine had five siblings – three brothers (George, Alexander and Paul, each of whom would become King of the Hellenes) and two sisters (Princess Helen, who married Crown Prince Carol of Romania, and Princess Irene who married Prince Aimone of Savoy, Duke of Spoleto).
They were reinstated following Alexander's death in 1920, but Constantine abdicated again in 1922.
The family moved to Villa Sparta in Florence, where Katherine took up painting.
Her second brother George became King George II in 1922, but was deposed in 1924.
Katherine was educated in England, at a boarding school at Broadstairs and then North Foreland Lodge.
She and the future Elizabeth II were bridesmaids at the wedding of her first cousin, Princess Marina, to Prince George in 1934.
Return to Greece and marriage

Her brother George was reinstated as king in 1935, and Katherine returned to Greece with her sister, Irene.
In 1941, after Greece had been overrun by Axis forces, she fled to South Africa with her third brother, Paul, in a Sunderland flying boat, where she worked as a nurse at a hospital in Cape Town.
On 1 April at the Royal Palace, three weeks prior to the wedding, her brother King George had a stroke and died shortly after in Katherine's presence.
George was succeeded on the Greek throne by Katherine's third brother Paul, who acted as best man at the wedding, which took place according to schedule on 21 April 1947.
On 25 August 1947, King George VI granted her the rank and title of a duke's daughter and she became known as Lady Katherine Brandram.
According to her obituary in The Daily Telegraph, "Lady Katherine lived quietly but remained in close touch with her own and the British royal families.
She attended the Queen's wedding to Prince Philip (her first cousin on her father’s side and second cousin once removed on her mother’s side), and was a guest at the service to mark Prince Philip's 80th birthday at St George's Chapel, Windsor, in 2001.
"


After the death of Infanta Beatriz of Spain in 2002, Katherine was the last surviving great-granddaughter of Queen Victoria, as well the last surviving grandchild of Frederick III, German Emperor and Victoria, Princess Royal.
Count Carl Johan Bernadotte of Sweden (31 October 1916 – 5 May 2012) as Queen Victoria's last living great-grandchild.
From the time of the death of her eldest sister Queen Helen, Queen Mother of Romania in 1982, to the time of her own death, she was Queen Victoria's most senior female line descendant.
Her death marked the end of all female-line direct descendants of Frederick III, German Emperor and Victoria, Princess Royal.
Issue

Princess Katherine of Greece and Denmark and Major Richard Campbell Andrew Brandram had one child, a son:


Bibliography

Ancestry

References

External links

@media screen{html.skin-theme-clientpref-night .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}} Media related to Princess Katherine of Greece and Denmark at Wikimedia Commons



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
  AssignClass (1864814f-1be3-4adb-8f16-8c770a616c63)
 Call ID: 1864814f-1be3-4adb-8f16-8c770a616c63
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    type: :Woman
  AssignClass (2740fa12-bbd3-4beb-8cc9-da63bdf18922)
 Call ID: 2740fa12-bbd3-4beb-8cc9-da63bdf18922
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    type: :Person
  AddLiteral (02e623d5-4f88-41e5-9472-ec7ca75f441a)
 Call ID: 02e623d5-4f88-41e5-9472-ec7ca75f441a
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1913
  AddLiteral (68040484-4813-4334-98b3-be13a8dedd3a)
 Call ID: 68040484-4813-4334-98b3-be13a8dedd3a
  Args:
    relation: :hasDeathYear
    literal_value: 2007
    literal_type: xsd:integer
    source: :Princess_Katherine_of_Greece_and_Denmark
  AddLiteral (4d4a3ceb-3aa8-4a92-b5d3-e51d581c4ee6)
 Call ID: 4d4a3ceb-3aa8-4a92-b5d3-e51d581c4ee6
  Args:
    literal_value: Lady Katherine Brandram
    relation: :knownAs
    source: :Princess_Katherine_of_Greece_and_Denmark
    literal_type: xsd:string
  AssignClass (b2528295-d809-4493-b583-39d43fa9fbf4)
 Call ID: b2528295-d809-4493-b583-39d43fa9fbf4
  Args:
    type: :Man
    source: :King_Constantine_I_of_Greece
  AssignClass (655dbde5-1b65-4ccc-9279-4c98f3110a14)
 Call ID: 655dbde5-1b65-4ccc-9279-4c98f3110a14
  Args:
    type: :Person
    source: :King_Constantine_I_of_Greece
  AssignClass (d00ebcf4-9b85-42e6-a335-29f71202c29c)
 Call ID: d00ebcf4-9b85-42e6-a335-29f71202c29c
  Args:
    type: :Woman
    source: :Princess_Sophia_of_Prussia
  AssignClass (3b786b8a-ac4f-48e4-8f5c-41fe0b385cc1)
 Call ID: 3b786b8a-ac4f-48e4-8f5c-41fe0b385cc1
  Args:
    type: :Person
    source: :Princess_Sophia_of_Prussia
  AddTriple (07149ee3-297c-4d6f-8ed9-66e91c7bbd15)
 Call ID: 07149ee3-297c-4d6f-8ed9-66e91c7bbd15
  Args:
    relation: :hasFather
    source: :Princess_Katherine_of_Greece_and_Denmark
    target: :King_Constantine_I_of_Greece
  AddTriple (0787ea13-515f-439d-b08f-d4a4ceb6eb63)
 Call ID: 0787ea13-515f-439d-b08f-d4a4ceb6eb63
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    target: :Princess_Sophia_of_Prussia
    relation: :hasMother
  AssignClass (11c98bae-9f07-479f-abc0-58b7031e6141)
 Call ID: 11c98bae-9f07-479f-abc0-58b7031e6141
  Args:
    source: :George_King_of_the_Hellenes
    type: :Man
  AssignClass (b97dc85e-e487-46da-8336-820aa7b1527b)
 Call ID: b97dc85e-e487-46da-8336-820aa7b1527b
  Args:
    type: :Person
    source: :George_King_of_the_Hellenes
  AssignClass (9221cb3a-0ffd-4b45-b851-52cdf4517ff1)
 Call ID: 9221cb3a-0ffd-4b45-b851-52cdf4517ff1
  Args:
    type: :Man
    source: :Alexander_King_of_the_Hellenes
  AssignClass (25b4e6dd-ee22-451a-9e71-f0d214a3b72b)
 Call ID: 25b4e6dd-ee22-451a-9e71-f0d214a3b72b
  Args:
    type: :Person
    source: :Alexander_King_of_the_Hellenes
  AssignClass (c750e35d-8af9-47a2-aa66-8ecb445d6cfe)
 Call ID: c750e35d-8af9-47a2-aa66-8ecb445d6cfe
  Args:
    type: :Man
    source: :Paul_King_of_the_Hellenes
  AssignClass (8eb99692-4fdb-4b75-b11e-31d720d2a397)
 Call ID: 8eb99692-4fdb-4b75-b11e-31d720d2a397
  Args:
    type: :Person
    source: :Paul_King_of_the_Hellenes
  AssignClass (20f2e502-ed1a-4189-b2d7-17e46f9ff03e)
 Call ID: 20f2e502-ed1a-4189-b2d7-17e46f9ff03e
  Args:
    type: :Woman
    source: :Princess_Helen_of_Greece_and_Denmark
  AssignClass (b7893bda-390a-42fa-8dbc-d8f35634decd)
 Call ID: b7893bda-390a-42fa-8dbc-d8f35634decd
  Args:
    source: :Princess_Helen_of_Greece_and_Denmark
    type: :Person
  AssignClass (b5cbe5cd-52a5-45f6-bfe9-58a122185d1e)
 Call ID: b5cbe5cd-52a5-45f6-bfe9-58a122185d1e
  Args:
    type: :Woman
    source: :Princess_Irene_of_Greece_and_Denmark
  AssignClass (bdb13afc-7655-4396-898b-4d8d55d48f0c)
 Call ID: bdb13afc-7655-4396-898b-4d8d55d48f0c
  Args:
    type: :Person
    source: :Princess_Irene_of_Greece_and_Denmark
  AddTriple (53664f11-5506-45b3-b896-57eb89bf7ec3)
 Call ID: 53664f11-5506-45b3-b896-57eb89bf7ec3
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    target: :George_King_of_the_Hellenes
    relation: :hasBrother
  AddTriple (30ce8efc-a306-437d-8d45-b558e31e270f)
 Call ID: 30ce8efc-a306-437d-8d45-b558e31e270f
  Args:
    relation: :hasBrother
    source: :Princess_Katherine_of_Greece_and_Denmark
    target: :Alexander_King_of_the_Hellenes
  AddTriple (ab2fd449-d7c9-4ab1-bec8-acb7fed5cdc8)
 Call ID: ab2fd449-d7c9-4ab1-bec8-acb7fed5cdc8
  Args:
    relation: :hasBrother
    target: :Paul_King_of_the_Hellenes
    source: :Princess_Katherine_of_Greece_and_Denmark
  AddTriple (2814f941-2b54-4f51-a8e0-b29e2582dc8f)
 Call ID: 2814f941-2b54-4f51-a8e0-b29e2582dc8f
  Args:
    target: :Princess_Helen_of_Greece_and_Denmark
    source: :Princess_Katherine_of_Greece_and_Denmark
    relation: :hasSister
  AddTriple (606560d4-049d-4551-99bd-2e3e522b095b)
 Call ID: 606560d4-049d-4551-99bd-2e3e522b095b
  Args:
    target: :Princess_Irene_of_Greece_and_Denmark
    source: :Princess_Katherine_of_Greece_and_Denmark
    relation: :hasSister
  AssignClass (b3abf115-02ca-429e-baa4-ed8356b9dd17)
 Call ID: b3abf115-02ca-429e-baa4-ed8356b9dd17
  Args:
    source: :Major_Richard_Campbell_Andrew_Brandram
    type: :Man
  AssignClass (75ccd929-906c-48df-ac4b-7bf01ac3a522)
 Call ID: 75ccd929-906c-48df-ac4b-7bf01ac3a522
  Args:
    source: :Major_Richard_Campbell_Andrew_Brandram
    type: :Person
  AddTriple (9cb928b2-6f74-4a32-8ee5-0ba9b28c14f2)
 Call ID: 9cb928b2-6f74-4a32-8ee5-0ba9b28c14f2
  Args:
    target: :Major_Richard_Campbell_Andrew_Brandram
    source: :Princess_Katherine_of_Greece_and_Denmark
    relation: :hasRelation
  Finish (2f826a19-62e1-485e-8352-8774b9eb1c16)
 Call ID: 2f826a19-62e1-485e-8352-8774b9eb1c16
  Args: