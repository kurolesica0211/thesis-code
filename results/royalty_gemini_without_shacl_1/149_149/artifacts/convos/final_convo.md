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
  AssignClass (b62cd548-e49a-45dd-882f-c57fce3643db)
 Call ID: b62cd548-e49a-45dd-882f-c57fce3643db
  Args:
    type: :Woman
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (08171ef3-a1e2-4df3-8a4f-46efef68f680)
 Call ID: 08171ef3-a1e2-4df3-8a4f-46efef68f680
  Args:
    type: :Person
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (cfce09c0-32f0-4801-b046-cc8d845b9884)
 Call ID: cfce09c0-32f0-4801-b046-cc8d845b9884
  Args:
    source: Alexandra_of_Greece_and_Denmark
    literal_value: Alexandra Georgievna
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddLiteral (24252b1b-1b4c-48cf-abfe-b0358c31f610)
 Call ID: 24252b1b-1b4c-48cf-abfe-b0358c31f610
  Args:
    source: Alexandra_of_Greece_and_Denmark
    literal_value: Aline
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (ef7a72a5-9184-4042-9652-7edda58768c5)
 Call ID: ef7a72a5-9184-4042-9652-7edda58768c5
  Args:
    literal_type: xsd:integer
    literal_value: 1870
    relation: :hasBirthYear
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (9850a11d-c735-4b1d-b17c-a503f2f46ff3)
 Call ID: 9850a11d-c735-4b1d-b17c-a503f2f46ff3
  Args:
    literal_type: xsd:integer
    literal_value: 1891
    relation: :hasDeathYear
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (aaecf83a-a1f4-4af0-9141-6e956254920a)
 Call ID: aaecf83a-a1f4-4af0-9141-6e956254920a
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (98be3562-f3b9-47e5-a025-a909dd228e92)
 Call ID: 98be3562-f3b9-47e5-a025-a909dd228e92
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (ade5e8bb-da9a-468c-a39b-11ab106dce82)
 Call ID: ade5e8bb-da9a-468c-a39b-11ab106dce82
  Args:
    source: George_I_of_Greece
    type: :Ancestor
  AssignClass (a85dd26a-03d0-4c0d-b2ad-45af33f27ac1)
 Call ID: a85dd26a-03d0-4c0d-b2ad-45af33f27ac1
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (4ce74480-b4b6-459e-a005-e02752c1b5f2)
 Call ID: 4ce74480-b4b6-459e-a005-e02752c1b5f2
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AssignClass (79e83ba3-3e07-4975-a892-d1e7bc0883c9)
 Call ID: 79e83ba3-3e07-4975-a892-d1e7bc0883c9
  Args:
    type: :Ancestor
    source: Olga_Constantinovna_of_Russia
  AddTriple (c07c2437-3fdf-470f-822b-ccfa62d9425e)
 Call ID: c07c2437-3fdf-470f-822b-ccfa62d9425e
  Args:
    source: Alexandra_of_Greece_and_Denmark
    target: George_I_of_Greece
    relation: :hasFather
  AddTriple (cd578340-4881-4f97-a10e-14f44008fc3f)
 Call ID: cd578340-4881-4f97-a10e-14f44008fc3f
  Args:
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (8f4d3336-7e8d-414f-abbc-57d5b71ec271)
 Call ID: 8f4d3336-7e8d-414f-abbc-57d5b71ec271
  Args:
    type: :Man
    source: Paul_Alexandrovich_of_Russia
  AssignClass (f593c9de-24ad-4777-b99d-cb7e789adf9b)
 Call ID: f593c9de-24ad-4777-b99d-cb7e789adf9b
  Args:
    source: Paul_Alexandrovich_of_Russia
    type: :Person
  AssignClass (13b04d83-8ca5-4f3a-9490-b59afb1aab80)
 Call ID: 13b04d83-8ca5-4f3a-9490-b59afb1aab80
  Args:
    source: Paul_Alexandrovich_of_Russia
    type: :Ancestor
  AddLiteral (f4ac9cfc-d102-4928-b25e-a7210370490a)
 Call ID: f4ac9cfc-d102-4928-b25e-a7210370490a
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1889
    source: Alexandra_of_Greece_and_Denmark
  AddTriple (780f468d-1f37-40d3-9a8f-2e6abceb0b4e)
 Call ID: 780f468d-1f37-40d3-9a8f-2e6abceb0b4e
  Args:
    relation: :hasRelation
    source: Alexandra_of_Greece_and_Denmark
    target: Paul_Alexandrovich_of_Russia
  AssignClass (9515fe12-0718-40df-8ad6-29e269927460)
 Call ID: 9515fe12-0718-40df-8ad6-29e269927460
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (245a9a9f-1a20-4573-9a1d-d4d760fef8b9)
 Call ID: 245a9a9f-1a20-4573-9a1d-d4d760fef8b9
  Args:
    source: Maria_Pavlovna
    type: :Person
  AssignClass (adfc8cb1-cbb1-40a3-a8f1-04f88b02271f)
 Call ID: adfc8cb1-cbb1-40a3-a8f1-04f88b02271f
  Args:
    source: Dmitri_Pavlovich
    type: :Man
  AssignClass (693cd503-2a89-4ec1-b1bb-8a6134dad8d7)
 Call ID: 693cd503-2a89-4ec1-b1bb-8a6134dad8d7
  Args:
    type: :Person
    source: Dmitri_Pavlovich
  AddTriple (500d6346-a33b-4828-8fef-ba4f23e78795)
 Call ID: 500d6346-a33b-4828-8fef-ba4f23e78795
  Args:
    relation: :hasChild
    source: Alexandra_of_Greece_and_Denmark
    target: Maria_Pavlovna
  AddTriple (54f0495e-001d-434a-b634-a192fdf32fd7)
 Call ID: 54f0495e-001d-434a-b634-a192fdf32fd7
  Args:
    relation: :hasChild
    source: Alexandra_of_Greece_and_Denmark
    target: Dmitri_Pavlovich
  AddTriple (84e0951e-e83a-48b6-90f1-df304d2af2c9)
 Call ID: 84e0951e-e83a-48b6-90f1-df304d2af2c9
  Args:
    relation: :hasChild
    source: Paul_Alexandrovich_of_Russia
    target: Maria_Pavlovna
  AddTriple (215aea49-7aa6-421c-ac7f-0e89d0d7209c)
 Call ID: 215aea49-7aa6-421c-ac7f-0e89d0d7209c
  Args:
    source: Paul_Alexandrovich_of_Russia
    target: Dmitri_Pavlovich
    relation: :hasChild
  AssignClass (43758dbc-7dc1-4be6-b96e-bfbb4d019912)
 Call ID: 43758dbc-7dc1-4be6-b96e-bfbb4d019912
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (e163a7c5-e1ae-4e17-a76f-50305c406132)
 Call ID: e163a7c5-e1ae-4e17-a76f-50305c406132
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (4081d90a-a685-4b54-a807-06953b867721)
 Call ID: 4081d90a-a685-4b54-a807-06953b867721
  Args:
    source: Christian_IX_of_Denmark
    type: :Ancestor
  AddTriple (ff4033dd-edc6-4337-8e7d-206425162288)
 Call ID: ff4033dd-edc6-4337-8e7d-206425162288
  Args:
    target: Christian_IX_of_Denmark
    source: George_I_of_Greece
    relation: :hasFather
  AssignClass (465aa670-1954-4abf-8246-7310817580bc)
 Call ID: 465aa670-1954-4abf-8246-7310817580bc
  Args:
    source: Alexander_II_of_Russia
    type: :Man
  AssignClass (31f423b3-2225-48d3-9ab5-298aa533e0b9)
 Call ID: 31f423b3-2225-48d3-9ab5-298aa533e0b9
  Args:
    source: Alexander_II_of_Russia
    type: :Person
  AssignClass (83bcb0c6-7c02-4ada-b47a-e1abb18db177)
 Call ID: 83bcb0c6-7c02-4ada-b47a-e1abb18db177
  Args:
    type: :Ancestor
    source: Alexander_II_of_Russia
  AssignClass (927ddcbc-f0fc-4b50-a610-b2b3d198af26)
 Call ID: 927ddcbc-f0fc-4b50-a610-b2b3d198af26
  Args:
    type: :Woman
    source: Marie_of_Hesse_and_by_Rhine
  AssignClass (8ddb7c57-6a26-4ad8-b450-fc903f0c5383)
 Call ID: 8ddb7c57-6a26-4ad8-b450-fc903f0c5383
  Args:
    type: :Person
    source: Marie_of_Hesse_and_by_Rhine
  AssignClass (d784ac8c-2801-4513-b07f-4f5acd61b727)
 Call ID: d784ac8c-2801-4513-b07f-4f5acd61b727
  Args:
    source: Marie_of_Hesse_and_by_Rhine
    type: :Ancestor
  AddTriple (9d54f6cc-abd8-40e1-9e1c-7cc9d14937f8)
 Call ID: 9d54f6cc-abd8-40e1-9e1c-7cc9d14937f8
  Args:
    relation: :hasFather
    target: Alexander_II_of_Russia
    source: Paul_Alexandrovich_of_Russia
  AddTriple (266be44e-e154-47d4-bf83-f937987903fa)
 Call ID: 266be44e-e154-47d4-bf83-f937987903fa
  Args:
    relation: :hasMother
    target: Marie_of_Hesse_and_by_Rhine
    source: Paul_Alexandrovich_of_Russia
  AssignClass (664a04ca-6f28-4bb5-9381-a3136babddc5)
 Call ID: 664a04ca-6f28-4bb5-9381-a3136babddc5
  Args:
    source: Nicholas_of_Greece
    type: :Man
  AssignClass (d873a358-7447-4043-8219-ce11c3f40311)
 Call ID: d873a358-7447-4043-8219-ce11c3f40311
  Args:
    type: :Person
    source: Nicholas_of_Greece
  AssignClass (6f03f276-ccbf-4afa-b23c-196db7746b6a)
 Call ID: 6f03f276-ccbf-4afa-b23c-196db7746b6a
  Args:
    type: :Woman
    source: Maria_of_Greece
  AssignClass (f8bfa816-b5f0-4905-9b4b-85b2e58f1580)
 Call ID: f8bfa816-b5f0-4905-9b4b-85b2e58f1580
  Args:
    type: :Person
    source: Maria_of_Greece
  AddTriple (011ef172-d865-43ad-8d0f-ca059c2a2063)
 Call ID: 011ef172-d865-43ad-8d0f-ca059c2a2063
  Args:
    source: Alexandra_of_Greece_and_Denmark
    target: Nicholas_of_Greece
    relation: :isSiblingOf
  AddTriple (39f16d20-a6bb-4a29-8cb6-5fd02006d02e)
 Call ID: 39f16d20-a6bb-4a29-8cb6-5fd02006d02e
  Args:
    relation: :isSiblingOf
    source: Alexandra_of_Greece_and_Denmark
    target: Maria_of_Greece
  Finish (16124b18-aa57-4299-84d9-5d83eca7a7e1)
 Call ID: 16124b18-aa57-4299-84d9-5d83eca7a7e1
  Args: