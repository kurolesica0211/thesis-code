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
Princess Alexandra of Greece and Denmark (Greek: Αλεξάνδρα; romanized: Alexándra), later known as Grand Duchess Alexandra Georgievna of Russia (Russian: Алекса́ндра Гео́ргиевна); 30 August  1870 – 24 September  1891), was a member of the Greek royal family by birth and of the Russian imperial family by marriage.
Alexandra was the daughter of George I of Greece and Olga Constantinovna of Russia, and grew up in Athens.
In 1889, she married Grand Duke Paul Alexandrovich of Russia, her first cousin once removed.
The couple settled in Saint Petersburg and they had two children: Grand Duchess Maria Pavlovna (1890–1958) and Grand Duke Dmitri Pavlovich (1891–1942).
Early life

Princess Alexandra of Greece and Denmark was born on 30 August  1870 at Mon Repos, the summer residence of the Greek royal family on the island of Corfu.
She was the third child and eldest daughter of King George I of Greece and his wife, Grand Duchess Olga Constantinovna of Russia.
Alexandra's father was not a native Greek, but he had been born a Danish prince named Christian Wilhelm of Schleswig-Holstein-Sonderburg-Glücksburg, a son of Christian IX, King of Denmark, and he had been elected to the Greek throne at the age of seventeen.
Five of his sons (Constantine, George, Nicholas, Andrew and Christopher), and two daughters (Alexandra and Maria), attained adulthood.
King George was a taciturn man, but contrary to the general approach of the time, he believed in happy rambunctious children.
The long corridors of the royal palace in Athens were used by Alexandra and her siblings for all types of play and sometimes a "bike ride" would be led by the King himself.
Alexandra, nicknamed "Aline" within her family, or Greek Alix, to distinguish her from her aunt and godmother, Alexandra, Princess of Wales, had a sunny disposition and was much loved by her family.
"


Alexandra's playmates were her brother Nicholas and her sister Maria, who followed her in age.
Alexandra spent many holidays in Denmark visiting her paternal grandparents.
In Denmark, Alexandra and her siblings met their Russian and British cousins in large family gatherings.
Marriage and children

When she was 18 years old, she was married to Grand Duke Paul Alexandrovich of Russia, her maternal first cousin once removed and the youngest child and sixth son of Emperor Alexander II and his first wife, Princess Marie of Hesse and by Rhine.
They had become close when Grand Duke Paul spent winters in Greece due to his frequent respiratory illnesses.
The Greek royal family also frequently spent holidays with the Romanov family on visits to Russia or Denmark.
They had two children:


Death

Seven months into her second pregnancy, Alexandra took a walk with her friends on the bank of the Moskva River and jumped directly into a boat that was permanently moored there, but fell as she got in.
The Grand Duchess was buried in the Peter and Paul Cathedral, St. Petersburg.
Her husband later morganatically remarried Olga Karnovich.
Alexandra's son would be involved in the murder of Grigori Rasputin, a friend of Tsarina Alexandra Feodorovna, in 1916.
In 1939 during the reign of her nephew George II of Greece, the Greek government obtained permission from the Soviet government under Joseph Stalin to rebury Princess Alexandra in Greece.
Alexandra's marble tombstone over an empty tomb is still in its place in the Peter and Paul Cathedral.
The "Alexandra Maternity Hospital" (now "Alexandra General Hospital") in Athens was later named in her memory by another nephew, King Paul; it was affiliated with the University of Athens with a special remit to research and combat postpartum maternal mortality.



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
  AssignClass (2c44a03c-8cc3-4718-b5cd-e330ef6eeb51)
 Call ID: 2c44a03c-8cc3-4718-b5cd-e330ef6eeb51
  Args:
    type: :Woman
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (04a83658-c52b-4782-af40-28b34fb03006)
 Call ID: 04a83658-c52b-4782-af40-28b34fb03006
  Args:
    type: :Person
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (d1a8f386-a237-47cc-8d11-1fc77db28aad)
 Call ID: d1a8f386-a237-47cc-8d11-1fc77db28aad
  Args:
    literal_type: xsd:string
    source: Alexandra_of_Greece_and_Denmark
    relation: :knownAs
    literal_value: Alexandra
  AddLiteral (7e32fa58-a1f8-427d-80dc-83603a22b545)
 Call ID: 7e32fa58-a1f8-427d-80dc-83603a22b545
  Args:
    literal_value: Grand Duchess Alexandra Georgievna of Russia
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (ba1cec51-9786-48ac-a34f-34dc99d55e4b)
 Call ID: ba1cec51-9786-48ac-a34f-34dc99d55e4b
  Args:
    relation: :hasBirthYear
    source: Alexandra_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1870
  AddLiteral (83153f0e-ecc7-4726-9f1a-9ace0b76d94f)
 Call ID: 83153f0e-ecc7-4726-9f1a-9ace0b76d94f
  Args:
    source: Alexandra_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1891
  AssignClass (871817d9-7f35-4ea4-a582-24be17200a48)
 Call ID: 871817d9-7f35-4ea4-a582-24be17200a48
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (08cf0ad5-97a3-4bb4-9bf0-2270e3e48464)
 Call ID: 08cf0ad5-97a3-4bb4-9bf0-2270e3e48464
  Args:
    type: :Ancestor
    source: George_I_of_Greece
  AssignClass (419d1f9e-d89d-475e-b2b9-c23e461dc240)
 Call ID: 419d1f9e-d89d-475e-b2b9-c23e461dc240
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (91ddb0c0-594f-4a82-84c9-29dbcade2ee2)
 Call ID: 91ddb0c0-594f-4a82-84c9-29dbcade2ee2
  Args:
    type: :Ancestor
    source: Olga_Constantinovna_of_Russia
  AddTriple (6b02262a-a605-4179-90e1-d65ce15b239e)
 Call ID: 6b02262a-a605-4179-90e1-d65ce15b239e
  Args:
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasFather
    target: George_I_of_Greece
  AddTriple (a228ce48-1de8-4cbe-a04c-60ff8351af28)
 Call ID: a228ce48-1de8-4cbe-a04c-60ff8351af28
  Args:
    target: Olga_Constantinovna_of_Russia
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (3f4da670-ede3-4dcf-979c-76cae4010a72)
 Call ID: 3f4da670-ede3-4dcf-979c-76cae4010a72
  Args:
    type: :Man
    source: Paul_Alexandrovich_of_Russia
  AddTriple (8ff38835-1528-40d7-810c-d600fe84b260)
 Call ID: 8ff38835-1528-40d7-810c-d600fe84b260
  Args:
    target: Paul_Alexandrovich_of_Russia
    relation: :hasRelation
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (6f7db826-7773-40e5-94f3-7a46339efac5)
 Call ID: 6f7db826-7773-40e5-94f3-7a46339efac5
  Args:
    source: Alexandra_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1889
  AssignClass (96dca55b-d25b-46a8-b55c-d49e4d28aa4b)
 Call ID: 96dca55b-d25b-46a8-b55c-d49e4d28aa4b
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (c9e55d67-5e95-4dff-be3f-bed7342e9121)
 Call ID: c9e55d67-5e95-4dff-be3f-bed7342e9121
  Args:
    type: :Person
    source: Maria_Pavlovna
  AssignClass (6810b55c-2dda-4aa9-86fb-9482c3694600)
 Call ID: 6810b55c-2dda-4aa9-86fb-9482c3694600
  Args:
    type: :Man
    source: Dmitri_Pavlovich
  AssignClass (bd1cd00b-251f-4ed5-a684-0ea1763c3985)
 Call ID: bd1cd00b-251f-4ed5-a684-0ea1763c3985
  Args:
    type: :Person
    source: Dmitri_Pavlovich
  AddTriple (b0d75d5e-db3a-4208-a5af-2aab4aa8ea3f)
 Call ID: b0d75d5e-db3a-4208-a5af-2aab4aa8ea3f
  Args:
    relation: :hasChild
    source: Alexandra_of_Greece_and_Denmark
    target: Maria_Pavlovna
  AddTriple (67b85d05-5d92-4c02-abac-f863d95acca2)
 Call ID: 67b85d05-5d92-4c02-abac-f863d95acca2
  Args:
    target: Dmitri_Pavlovich
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasChild
  AddTriple (e3dc12ef-7cc8-4833-af21-014e4c5a71ba)
 Call ID: e3dc12ef-7cc8-4833-af21-014e4c5a71ba
  Args:
    relation: :hasFather
    source: Maria_Pavlovna
    target: Paul_Alexandrovich_of_Russia
  AddTriple (7b5dbba5-5267-4325-9d59-a16989f589a1)
 Call ID: 7b5dbba5-5267-4325-9d59-a16989f589a1
  Args:
    relation: :hasFather
    source: Dmitri_Pavlovich
    target: Paul_Alexandrovich_of_Russia
  AddTriple (073cdeb9-8af5-47e3-9096-afc25609cb2a)
 Call ID: 073cdeb9-8af5-47e3-9096-afc25609cb2a
  Args:
    target: Alexandra_of_Greece_and_Denmark
    source: Maria_Pavlovna
    relation: :hasMother
  AddTriple (6c7a9c64-5f6f-4e81-a10a-386f3ead3b45)
 Call ID: 6c7a9c64-5f6f-4e81-a10a-386f3ead3b45
  Args:
    relation: :hasMother
    source: Dmitri_Pavlovich
    target: Alexandra_of_Greece_and_Denmark
  AssignClass (fb534d92-9a06-4252-a07f-9312208b5acc)
 Call ID: fb534d92-9a06-4252-a07f-9312208b5acc
  Args:
    type: :Man
    source: Nicholas_of_Greece
  AssignClass (cbdc6336-404b-43eb-a636-6741413e069b)
 Call ID: cbdc6336-404b-43eb-a636-6741413e069b
  Args:
    type: :Person
    source: Nicholas_of_Greece
  AssignClass (a2787e65-1b40-4466-969d-4300a6486422)
 Call ID: a2787e65-1b40-4466-969d-4300a6486422
  Args:
    type: :Woman
    source: Maria_of_Greece
  AssignClass (d36313ad-f2a3-4375-99d9-161aa816776c)
 Call ID: d36313ad-f2a3-4375-99d9-161aa816776c
  Args:
    type: :Person
    source: Maria_of_Greece
  AddTriple (b2fdc3f1-92af-49b3-8ea4-df9cdb62e289)
 Call ID: b2fdc3f1-92af-49b3-8ea4-df9cdb62e289
  Args:
    target: Nicholas_of_Greece
    source: Alexandra_of_Greece_and_Denmark
    relation: :isSiblingOf
  AddTriple (c8572df7-17ef-4b71-94ec-3255d1bb7f94)
 Call ID: c8572df7-17ef-4b71-94ec-3255d1bb7f94
  Args:
    target: Maria_of_Greece
    relation: :isSiblingOf
    source: Alexandra_of_Greece_and_Denmark
  Finish (eea3063f-cee5-433b-a308-1ae6fb75d774)
 Call ID: eea3063f-cee5-433b-a308-1ae6fb75d774
  Args: