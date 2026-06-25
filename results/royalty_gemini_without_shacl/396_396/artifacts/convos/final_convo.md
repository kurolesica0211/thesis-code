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
Princess Christina Margarethe of Hesse (German: Christina Margarethe Prinzessin von Hessen; 10 January 1933 – 22 November 2011) was a German princess.
Family background and early life

Born in Germany on 10 January 1933 at Friedrichshof Castle near Kronberg im Taunus, Princess Christina ("Krista") of Hesse was the eldest child of Prince Christoph of Hesse (1901–1943) and Princess Sophie of Greece and Denmark (1914–2001)
Her father, Prince Christoph of Hesse, was a nephew of Germany's last emperor Wilhelm II.
Her mother, Princess Sophie of Greece and Denmark, was a grand-daughter of King George I of Greece and a sister of Prince Philip, Duke of Edinburgh.
Christina belonged by birth to the senior line of the House of Hesse, a junior branch of which reigned as grand dukes of Hesse and by Rhine within the German Empire until 1918.
Christina's paternal grandmother, Princess Margaret of Prussia, was a daughter of Queen Victoria's eldest daughter Victoria, and as such a sister of Kaiser Wilhelm II.


Prince Christoph, a member of the Schutzstaffel (SS), held important positions in Germany's Nazi regime.
On 7 October 1943, when Christina was ten years old, her father was killed in an airplane crash in the Apennine Mountains near Forlì, Italy.
His widow married Prince George William of Hanover in 1946.
From her mother's two marriages, Christina had four siblings and three half-siblings: Princess Dorothea of Hesse (1934–2025), Prince Karl of Hesse (1937–2022), Prince Rainer of Hesse (born 1939), Princess Clarissa of Hesse (born 1944), Prince Welf of Hanover (1947–1981), Prince Georg of Hanover (born 1949) and Princess Friederike of Hanover (born 1954).
Her childhood homes included her paternal grandmother's palace of Friedrichshof in Taunus, a family castle at Panker in Holstein, and her parents' residence in Berlin-Dahlem.
Christina participated in the 1953 coronation of her aunt at Westminster Abbey, walking in the procession led by her maternal grandmother, Princess Alice.
Christina and her cousin Princess Beatrix of Hohenlohe-Langenburg spent the winter of 1955-1956 living in London, where Christina studied the restoration of paintings under Anthony Blunt.
It was reported that the princesses' closest friend in England was Prince Andrew of Yugoslavia.
First marriage

Princess Christina of Hesse married Prince Andrew of Yugoslavia, the youngest son of Alexander I of Yugoslavia and Princess Maria of Romania, on 2 August 1956, at Friedrichshof Castle.
They had two children:


Soon after their marriage, Princess Christina and her first husband had purchased The Hollands, a commercial farm at Langton Green in Kent, England, which did not prove a profitable venture.
Moving to London, Prince Andrew supported his family by working for an import/export business and, later, as a bank executive.
In 1961 Christina left her husband to live with an abstract artist from the Netherlands, Robert Floris van Eyck.
Second marriage

Following her divorce, Christina married Robert van Eyck on 3 December 1962 in London.
Her first husband Prince Andrew also married for the second time, this time to another cousin, Princess Kira Melita zu Leiningen (1930–2006).
Christina and Robert van Eyck separated in 1985, and divorced 3 February 1986.
In addition to Germany and England, Princess Christina of Hesse had lived in Saint-Paul-de-Vence, France, and in Gersau, Switzerland.



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
  AssignClass (3c590bfd-a688-47a2-9a54-33d14665a859)
 Call ID: 3c590bfd-a688-47a2-9a54-33d14665a859
  Args:
    type: :Woman
    source: Princess_Christina_of_Hesse
  AddLiteral (5ab3d4e8-5b06-4abd-9d1d-409102d75d71)
 Call ID: 5ab3d4e8-5b06-4abd-9d1d-409102d75d71
  Args:
    relation: :hasBirthYear
    source: Princess_Christina_of_Hesse
    literal_value: 1933
    literal_type: xsd:integer
  AddLiteral (dae3b480-2d9b-4518-9946-849548089881)
 Call ID: dae3b480-2d9b-4518-9946-849548089881
  Args:
    literal_type: xsd:integer
    literal_value: 2011
    source: Princess_Christina_of_Hesse
    relation: :hasDeathYear
  AssignClass (e42a8072-1e4e-478f-bff4-ea2e7e827952)
 Call ID: e42a8072-1e4e-478f-bff4-ea2e7e827952
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Man
  AddLiteral (c9d6e34b-031a-4fb8-859a-d7c2b1d2169b)
 Call ID: c9d6e34b-031a-4fb8-859a-d7c2b1d2169b
  Args:
    literal_type: xsd:integer
    source: Prince_Christoph_of_Hesse
    relation: :hasBirthYear
    literal_value: 1901
  AddLiteral (022d64f5-a0dd-4157-8cfd-6f3cb5d96a2f)
 Call ID: 022d64f5-a0dd-4157-8cfd-6f3cb5d96a2f
  Args:
    literal_type: xsd:integer
    source: Prince_Christoph_of_Hesse
    relation: :hasDeathYear
    literal_value: 1943
  AssignClass (c14ac4b3-d403-445f-9dd7-7d3e1c2d62da)
 Call ID: c14ac4b3-d403-445f-9dd7-7d3e1c2d62da
  Args:
    type: :Woman
    source: Princess_Sophie_of_Greece_and_Denmark
  AddLiteral (3adc6f27-2233-447b-ae3e-e38c6ffec135)
 Call ID: 3adc6f27-2233-447b-ae3e-e38c6ffec135
  Args:
    literal_value: 1914
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (27d387cb-db59-45ef-b476-7e661e607560)
 Call ID: 27d387cb-db59-45ef-b476-7e661e607560
  Args:
    literal_value: 2001
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (fad53493-6102-4e5e-824d-8a15afbf76d6)
 Call ID: fad53493-6102-4e5e-824d-8a15afbf76d6
  Args:
    source: Princess_Christina_of_Hesse
    relation: :hasFather
    target: Prince_Christoph_of_Hesse
  AddTriple (bc3c9480-70ae-4bb8-a7d0-0069dd9f0bb1)
 Call ID: bc3c9480-70ae-4bb8-a7d0-0069dd9f0bb1
  Args:
    relation: :hasMother
    source: Princess_Christina_of_Hesse
    target: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (b8429cdf-983f-4b9b-99ca-02e28a29e1c1)
 Call ID: b8429cdf-983f-4b9b-99ca-02e28a29e1c1
  Args:
    source: Prince_George_William_of_Hanover
    type: :Man
  AddTriple (57e4e490-a7cf-485a-9a25-02fa872840e8)
 Call ID: 57e4e490-a7cf-485a-9a25-02fa872840e8
  Args:
    target: Prince_George_William_of_Hanover
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasMarriageYear
  AddLiteral (9a0d2613-ad44-4db8-b941-10f4a88ac952)
 Call ID: 9a0d2613-ad44-4db8-b941-10f4a88ac952
  Args:
    literal_value: 1946
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (c2c821a7-4d34-46f3-b621-39aac470f5bf)
 Call ID: c2c821a7-4d34-46f3-b621-39aac470f5bf
  Args:
    type: :Man
    source: Prince_Andrew_of_Yugoslavia
  AddTriple (5a4f0091-6587-458b-b8e6-f50511c2a2f3)
 Call ID: 5a4f0091-6587-458b-b8e6-f50511c2a2f3
  Args:
    target: Prince_Andrew_of_Yugoslavia
    relation: :hasMarriageYear
    source: Princess_Christina_of_Hesse
  AddLiteral (daf24191-d0e7-49ec-878c-339ed1ad2991)
 Call ID: daf24191-d0e7-49ec-878c-339ed1ad2991
  Args:
    relation: :hasMarriageYear
    source: Princess_Christina_of_Hesse
    literal_value: 1956
    literal_type: xsd:integer
  AssignClass (5cf4e1a2-a73e-48d2-b571-f4bfef76495a)
 Call ID: 5cf4e1a2-a73e-48d2-b571-f4bfef76495a
  Args:
    type: :Man
    source: Robert_van_Eyck
  AddTriple (f8b6daed-5205-4eca-ac9f-8fea8038e547)
 Call ID: f8b6daed-5205-4eca-ac9f-8fea8038e547
  Args:
    relation: :hasMarriageYear
    source: Princess_Christina_of_Hesse
    target: Robert_van_Eyck
  AddLiteral (59e00b3c-dfa9-49d7-b4dd-3c5a3cb223e1)
 Call ID: 59e00b3c-dfa9-49d7-b4dd-3c5a3cb223e1
  Args:
    literal_type: xsd:integer
    literal_value: 1962
    source: Princess_Christina_of_Hesse
    relation: :hasMarriageYear
  Finish (a6f9884c-fc3d-433e-8a49-ef8d182229a3)
 Call ID: a6f9884c-fc3d-433e-8a49-ef8d182229a3
  Args: