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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (4ed28f3a-71a0-4819-9492-34d9ae334557)
 Call ID: 4ed28f3a-71a0-4819-9492-34d9ae334557
  Args:
    source: Alexandra_of_Greece_and_Denmark
    type: :Woman
  AssignClass (5f0cae98-4d8d-48cd-bbc3-42a6897da466)
 Call ID: 5f0cae98-4d8d-48cd-bbc3-42a6897da466
  Args:
    source: Alexandra_of_Greece_and_Denmark
    type: :Person
  AddLiteral (dbfadffb-5fb2-4edd-aa00-4f91e2aa150c)
 Call ID: dbfadffb-5fb2-4edd-aa00-4f91e2aa150c
  Args:
    relation: :alsoKnownAs
    source: Alexandra_of_Greece_and_Denmark
    literal_value: Grand Duchess Alexandra Georgievna of Russia
    literal_type: xsd:string
  AddLiteral (2c549956-99bf-4923-82f5-2a4b69b1a4f7)
 Call ID: 2c549956-99bf-4923-82f5-2a4b69b1a4f7
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1870
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (97f704c3-94be-40dd-b84c-1b0a8ccadcad)
 Call ID: 97f704c3-94be-40dd-b84c-1b0a8ccadcad
  Args:
    literal_value: 1891
    source: Alexandra_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (ba8a8dc7-e9ed-41f1-a299-ed39393bede6)
 Call ID: ba8a8dc7-e9ed-41f1-a299-ed39393bede6
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (59742528-3acd-48a9-a201-0dd47bd7d4b2)
 Call ID: 59742528-3acd-48a9-a201-0dd47bd7d4b2
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (5e944ace-0c09-438e-8c08-74873f672470)
 Call ID: 5e944ace-0c09-438e-8c08-74873f672470
  Args:
    type: :Ancestor
    source: George_I_of_Greece
  AssignClass (eb4f022f-e889-4c4f-a1cc-03a4baa9b292)
 Call ID: eb4f022f-e889-4c4f-a1cc-03a4baa9b292
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (4e92f7db-afba-486f-b7a7-3c1d211933cc)
 Call ID: 4e92f7db-afba-486f-b7a7-3c1d211933cc
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AssignClass (1d9a7392-561b-4639-8e9e-d525a2e89fb6)
 Call ID: 1d9a7392-561b-4639-8e9e-d525a2e89fb6
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Ancestor
  AddTriple (72da154e-ed7e-42f2-9f61-4c3c20a8e16a)
 Call ID: 72da154e-ed7e-42f2-9f61-4c3c20a8e16a
  Args:
    relation: :hasFather
    target: George_I_of_Greece
    source: Alexandra_of_Greece_and_Denmark
  AddTriple (fd7f4787-69a3-4385-8501-da1d3c1a3cf9)
 Call ID: fd7f4787-69a3-4385-8501-da1d3c1a3cf9
  Args:
    relation: :hasMother
    source: Alexandra_of_Greece_and_Denmark
    target: Olga_Constantinovna_of_Russia
  AssignClass (f0aedb5e-c719-4667-9633-9d153c8140b5)
 Call ID: f0aedb5e-c719-4667-9633-9d153c8140b5
  Args:
    type: :Man
    source: Paul_Alexandrovich_of_Russia
  AssignClass (093aee56-15a1-4af8-898c-4ba0f574a1ee)
 Call ID: 093aee56-15a1-4af8-898c-4ba0f574a1ee
  Args:
    type: :Person
    source: Paul_Alexandrovich_of_Russia
  AssignClass (8e79ec2d-6103-40e3-81bc-967e6d6cb1d8)
 Call ID: 8e79ec2d-6103-40e3-81bc-967e6d6cb1d8
  Args:
    type: :Ancestor
    source: Paul_Alexandrovich_of_Russia
  AddLiteral (8233a9d5-0aa5-4c5a-9215-dc286c728311)
 Call ID: 8233a9d5-0aa5-4c5a-9215-dc286c728311
  Args:
    literal_value: 1889
    source: Alexandra_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (736a24cf-b29f-4d03-977d-485d8ff759ee)
 Call ID: 736a24cf-b29f-4d03-977d-485d8ff759ee
  Args:
    relation: :hasRelation
    source: Alexandra_of_Greece_and_Denmark
    target: Paul_Alexandrovich_of_Russia
  AssignClass (d3df3f01-c379-45e0-904c-785c64aab5f9)
 Call ID: d3df3f01-c379-45e0-904c-785c64aab5f9
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (0b1108a0-8481-4cf2-9ebe-494452ef0d72)
 Call ID: 0b1108a0-8481-4cf2-9ebe-494452ef0d72
  Args:
    source: Maria_Pavlovna
    type: :Person
  AssignClass (fc647948-e07e-4e77-9015-b941d1073e82)
 Call ID: fc647948-e07e-4e77-9015-b941d1073e82
  Args:
    type: :Man
    source: Dmitri_Pavlovich
  AssignClass (f456bd40-0c8e-46d4-a60b-8020268bd4a8)
 Call ID: f456bd40-0c8e-46d4-a60b-8020268bd4a8
  Args:
    source: Dmitri_Pavlovich
    type: :Person
  AddTriple (7780b421-9bee-4a8f-9fea-8dba0f1c2517)
 Call ID: 7780b421-9bee-4a8f-9fea-8dba0f1c2517
  Args:
    relation: :hasChild
    target: Maria_Pavlovna
    source: Alexandra_of_Greece_and_Denmark
  AddTriple (520566a4-c9b4-4abf-884d-f0a0034ff1dd)
 Call ID: 520566a4-c9b4-4abf-884d-f0a0034ff1dd
  Args:
    relation: :hasChild
    source: Alexandra_of_Greece_and_Denmark
    target: Dmitri_Pavlovich
  AddTriple (6b14170f-7270-4823-b3c9-e64d1c5772ab)
 Call ID: 6b14170f-7270-4823-b3c9-e64d1c5772ab
  Args:
    relation: :hasChild
    source: Paul_Alexandrovich_of_Russia
    target: Maria_Pavlovna
  AddTriple (7680f71f-731d-4b00-96bc-8bc044c14714)
 Call ID: 7680f71f-731d-4b00-96bc-8bc044c14714
  Args:
    relation: :hasChild
    target: Dmitri_Pavlovich
    source: Paul_Alexandrovich_of_Russia
  AssignClass (79e77df9-a951-494a-be73-a687c79be755)
 Call ID: 79e77df9-a951-494a-be73-a687c79be755
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (6a483957-dc7c-4d2b-9ff0-4605ebca0bd2)
 Call ID: 6a483957-dc7c-4d2b-9ff0-4605ebca0bd2
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AssignClass (1bd3c2b2-45d0-4793-9fdc-acbb08e1858a)
 Call ID: 1bd3c2b2-45d0-4793-9fdc-acbb08e1858a
  Args:
    type: :Ancestor
    source: Christian_IX_of_Denmark
  AddTriple (a2e4fa90-bb34-45e7-9c4c-a2b750d1e733)
 Call ID: a2e4fa90-bb34-45e7-9c4c-a2b750d1e733
  Args:
    relation: :hasFather
    source: George_I_of_Greece
    target: Christian_IX_of_Denmark
  AssignClass (a9838030-54e5-47e8-b57f-30a84f215eef)
 Call ID: a9838030-54e5-47e8-b57f-30a84f215eef
  Args:
    type: :Man
    source: Constantine_of_Greece
  AssignClass (c4d6f3b8-924b-4fff-a933-8147a0c69db8)
 Call ID: c4d6f3b8-924b-4fff-a933-8147a0c69db8
  Args:
    source: Constantine_of_Greece
    type: :Person
  AssignClass (aefe308e-c59f-4a60-bfe3-161953d781b3)
 Call ID: aefe308e-c59f-4a60-bfe3-161953d781b3
  Args:
    type: :Man
    source: Nicholas_of_Greece
  AssignClass (4ba951bc-a1ae-4ad1-b831-e943aa992515)
 Call ID: 4ba951bc-a1ae-4ad1-b831-e943aa992515
  Args:
    type: :Person
    source: Nicholas_of_Greece
  AssignClass (89aa22ab-1f85-42bf-bb68-e8683d14fc7e)
 Call ID: 89aa22ab-1f85-42bf-bb68-e8683d14fc7e
  Args:
    source: Andrew_of_Greece
    type: :Man
  AssignClass (7f4dda74-6139-42cb-a5d0-23e8b16b39cd)
 Call ID: 7f4dda74-6139-42cb-a5d0-23e8b16b39cd
  Args:
    source: Andrew_of_Greece
    type: :Person
  AssignClass (a8cfc15f-b91e-4a09-adf1-d7a129ea408c)
 Call ID: a8cfc15f-b91e-4a09-adf1-d7a129ea408c
  Args:
    type: :Man
    source: Christopher_of_Greece
  AssignClass (eafac417-510d-4a42-99a2-3642ed2b09ed)
 Call ID: eafac417-510d-4a42-99a2-3642ed2b09ed
  Args:
    source: Christopher_of_Greece
    type: :Person
  AssignClass (e03eeb38-f701-47a1-a441-c503f49a5c2e)
 Call ID: e03eeb38-f701-47a1-a441-c503f49a5c2e
  Args:
    type: :Woman
    source: Maria_of_Greece
  AssignClass (152529f9-2bb0-4141-a260-8aa1e002bef9)
 Call ID: 152529f9-2bb0-4141-a260-8aa1e002bef9
  Args:
    source: Maria_of_Greece
    type: :Person
  AddTriple (1b320389-fe54-4488-98c1-1fb7483feb42)
 Call ID: 1b320389-fe54-4488-98c1-1fb7483feb42
  Args:
    target: Constantine_of_Greece
    source: George_I_of_Greece
    relation: :hasChild
  AddTriple (a03ea47c-5068-4f3f-9a66-f7c733449ea4)
 Call ID: a03ea47c-5068-4f3f-9a66-f7c733449ea4
  Args:
    target: Nicholas_of_Greece
    source: George_I_of_Greece
    relation: :hasChild
  AddTriple (9e8b24dd-0eae-40df-be37-5aad4bfa3c34)
 Call ID: 9e8b24dd-0eae-40df-be37-5aad4bfa3c34
  Args:
    relation: :hasChild
    target: Andrew_of_Greece
    source: George_I_of_Greece
  AddTriple (258e67aa-b85f-49a5-8e2f-9504fa799f40)
 Call ID: 258e67aa-b85f-49a5-8e2f-9504fa799f40
  Args:
    source: George_I_of_Greece
    target: Christopher_of_Greece
    relation: :hasChild
  AddTriple (2714d991-013e-434c-9eb5-144f0d1548ae)
 Call ID: 2714d991-013e-434c-9eb5-144f0d1548ae
  Args:
    relation: :hasChild
    target: Maria_of_Greece
    source: George_I_of_Greece
  AssignClass (5cbadcaf-1684-4441-a473-c863f794e7f9)
 Call ID: 5cbadcaf-1684-4441-a473-c863f794e7f9
  Args:
    type: :Man
    source: Alexander_II_of_Russia
  AssignClass (299e4331-a872-440a-a982-8732dfec88d4)
 Call ID: 299e4331-a872-440a-a982-8732dfec88d4
  Args:
    type: :Person
    source: Alexander_II_of_Russia
  AssignClass (973a2874-ff4c-4029-87df-0b7ebf0585d7)
 Call ID: 973a2874-ff4c-4029-87df-0b7ebf0585d7
  Args:
    type: :Ancestor
    source: Alexander_II_of_Russia
  AssignClass (dd4dcbf6-fb41-414b-8d82-a7349873d089)
 Call ID: dd4dcbf6-fb41-414b-8d82-a7349873d089
  Args:
    source: Marie_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (6e122a51-29e4-4e07-9499-a4b9c6624983)
 Call ID: 6e122a51-29e4-4e07-9499-a4b9c6624983
  Args:
    source: Marie_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (9fcf2750-6248-43e9-90e9-369548fb3fce)
 Call ID: 9fcf2750-6248-43e9-90e9-369548fb3fce
  Args:
    source: Marie_of_Hesse_and_by_Rhine
    type: :Ancestor
  AddTriple (ffcf9333-9f87-49b4-b600-077cd11229f2)
 Call ID: ffcf9333-9f87-49b4-b600-077cd11229f2
  Args:
    target: Alexander_II_of_Russia
    source: Paul_Alexandrovich_of_Russia
    relation: :hasFather
  AddTriple (4ef791ea-015b-4c62-ac2b-4916728e1a2a)
 Call ID: 4ef791ea-015b-4c62-ac2b-4916728e1a2a
  Args:
    target: Marie_of_Hesse_and_by_Rhine
    source: Paul_Alexandrovich_of_Russia
    relation: :hasMother
  AssignClass (096c47fc-e4a9-42f9-83ea-4b466ea068f7)
 Call ID: 096c47fc-e4a9-42f9-83ea-4b466ea068f7
  Args:
    source: Olga_Karnovich
    type: :Woman
  AssignClass (8139e279-91b9-4dcd-a2ee-b5308c6c733a)
 Call ID: 8139e279-91b9-4dcd-a2ee-b5308c6c733a
  Args:
    source: Olga_Karnovich
    type: :Person
  AddTriple (51d8a619-61f4-4692-bf04-21a94ec8b4ba)
 Call ID: 51d8a619-61f4-4692-bf04-21a94ec8b4ba
  Args:
    target: Olga_Karnovich
    source: Paul_Alexandrovich_of_Russia
    relation: :hasRelation
  Finish (23c223fe-150e-40eb-83cb-9e3e63a28928)
 Call ID: 23c223fe-150e-40eb-83cb-9e3e63a28928
  Args: