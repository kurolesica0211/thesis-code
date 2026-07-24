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
Henri d'Orléans (Henri Robert Ferdinand Marie d'Orléans; 5 July 1908 – 19 June 1999), was the Orléanist pretender to the defunct throne of France as Henry VI from 1940 until his death in 1999.
Henri was the direct descendant of Philippe I, Duke of Orléans, son of Louis XIII.
He was also a descendant of Louis XIV through a female line, from his legitimized daughter Françoise Marie de Bourbon, as well as the great-great-grandson, by four different lines of descent, of Louis Philippe I.
The son of Jean, Duke of Guise, Henri was forbidden to enter France for much of his life.
Henri worked to restore the French monarchy in a parliamentary form, and discussed the topic with Charles de Gaulle.
Upon his death in 1999, his son Henri succeeded him as Head of the House of Orléans.
Here, Henri rose at 4 am daily, accompanying his father to oversee livestock management and crop production on their scattered lands, later in the day being tutored by European governesses and his mother: He acquired fluency in French, Arabic, English, German, Italian and Spanish.
Being rebuffed by France, Belgium and the United Kingdom, Prince Jean finally took his family back to Morocco and farming.
In 1921, Henri's governesses were replaced with a series of preceptors, all coming from France.
In 1923, the abbé Thomas took over Henri's instruction and, being less traditional in his approach, awakened in his charge a hitherto undetected thirst for knowledge.
Using the wedding of the prince's sister that year in France as an opportunity, Thomas obtained permission to take Henri to the Parisian banlieues of Meudon and Issy-les-Moulineaux, then working class slums in which the abbé would volunteer to serve the needy daily, bringing Henri into close contact with day laborers.
He would later write that this wretched urban experience profoundly affected his future political outlook and sense of justice, contrasting unfavourably with the deprivation to which he was accustomed in Morocco where, he observed, the poor were at least able to enjoy fresh air, space and sunlight while surrounded by relatives and neighbors who shared a near universal poverty, compared to the depressing grime, crowded conditions and anonymity in which Parisian workers toiled amidst extremes of wealth and deprivation.
After a year Thomas, whose health suffered in Morocco, was replaced as Henri's preceptor by abbé Dartein, who accompanied the family to France in 1924, preparing the prince for his collegiate matriculation while they occupied an apartment near his parents in Paris.
Henri began a two-year study of mathematics and the sciences at the Catholic University of Louvain in 1924, studying the law for the two years following.
From across the border in France came scholars and veterans of renown to coach Henri for his future role as a royalist leader, including jurist Ernest Perrot, military strategist Général Henri de Gondrecourt and the diplomat Charles Benoist, a member of the Académie des Sciences Morales et Politiques who would serve as his advisor from 1930.
Dauphin in pretence

In 1926, Henri became the Dauphin of France in pretence when his father became the Orléanist claimant to the defunct throne upon the death of his maternal uncle, Philippe, Duke of Orleans.
In 1939, after being refused admission to both the French and the British armed forces, Henri was allowed to join the French Foreign Legion.
Orléanist pretender

World War II

Henri became pretender to the defunct French throne on 25 August 1940 when his father died.
Henri was a "gentlemen farmer" in Morocco in the course of 1942.
In mid-November 1942, after Admiral François Darlan's armistice with the Allied invaders of North Africa, Vichy intelligence official Henri d'Astier de la Vigerie attempted to promote a royalist coup (d'Astier had previously conspired with the Allies to aid the invasion).
He proposed that Henri would appear to head a French government composed of all political tendencies, and maintain "neutrality until the day comes when the French nation can freely decide for itself."
Ridgeway was taken aback by the proposal, but was unaware that d'Astier's colleagues, Abbé Cordier and Master-Sergeant Sabatier (a French instructor at an OSS-SOE camp in Algiers), had secretly brought Henri from Morocco to d'Astier's apartment in Algiers.
Post war

In 1947, Henri and his family took up residence at the Quinta do Anjinho, an estate in Sintra, on the Portuguese Riviera.
In 1950, after the law of exile was rescinded, Henri returned to France.
During his tenure as pretender to the defunct throne, Henri used the majority of his family's great wealth, selling off family jewels, paintings, furniture and properties to support his political cause and large family, as well as establishments in Belgium, North Africa, Brazil, Portugal and France.
Political activity

Unlike his father, Henri devoted his life to politics.
During World War II, Henri was initially sympathetic to Vichy France.
His opinions on the government changed over time, and he contacted Prime Minister Pierre Laval.
Laval offered Henri the unglamorous position of Minister of Food, which he declined.
In Algeria, Henri attempted to convince the French military governor not to oppose an Anglo-American military landing.
Henri had correctly predicted such a thing occurring, but at the time he was laughed at by the officers.
Henri also tried to mediate between Charles de Gaulle and Henri Giraud, when the two men were competing for control of Free France.
Between 1940 and 1941, the Gaullist camp offered Henri an invitation to go to London, which he declined.
Henri feared that if he accepted the offer, he would have become an émigré, like the Bourbons who returned to France after Napoleon's defeat.
Henri was staunchly opposed to the idea of siding with one political party, wishing instead to pursue a path of unity and not contribute to France's "infernal divisiveness."
"


In 1948, Henri began publishing a monthly bulletin, which soon possessed 30,000 subscribers.
In 1950, the French Parliament abrogated the Law of Exile, permitting Henri to return.
So we have to make do with Henri, who strikes a royal enough pose, I guess.
In 1954, Henri met Charles de Gaulle and continued their relationship through correspondence.
In 1958, Henri gave his support to de Gaulle, who was called back from his self-imposed exile to save the French Republic from insurrection in Paris.
Thereafter, Henri became a frequent visitor to the Élysée Palace, where de Gaulle waited for Henri "by the staircase or outside, reserved a special armchair for him and lit his cigarette."
There, they frequently discussed French history together, with Henri noting that de Gaulle loved to pronounce the word 'king'.
In 1960, de Gaulle told Henri that "Monseigneur, I believe deeply in the value of the monarchy, and I am certain as well that this regime is the one best suited to our poor country."
The following year, de Gaulle dispatched Henri on a tour to Libya, Ethiopia, Iran, and Lebanon, with the purpose of explaining France's Algeria policy, serving as de Gaulle's special representative, or "pro-consul."
During this time, Henri befriended Hassan II of Morocco and Habib Bourguiba.
In 1962, de Gaulle informed Henri in strict confidence that he had arranged the French presidential election so that the head of the royal house could succeed him as president of the Republic.
However, by 1964, de Gaulle changed his mind and told Henri of his decision to run for re-election, which he won.
By 1968, Henri ceased publication of his paper over his increasing disagreements with the Gaullists.
The Countess of Paris remarked that "Under de Gaulle, Henri came two fingers close to becoming king.
"


Following de Gaulle's death in 1970, his son Philippe de Gaulle told Henri, "Monseigneur, my father often told me that if circumstances had been different, he would have been happy to be your faithful and loyal servant."
In 1979, Henri published his book Mémoires d'exil et de combats, which revealed to the public that de Gaulle had asked Henri to prepare himself for the 1965 presidential elections in France.
In a latter interview, Henri stated "At all times de Gaulle desired restoration, I am convinced of it.
However, Henri also noted that "It was difficult to get anywhere without de Gaulle, He agreed to favor my ascension to the highest point, but he didn't understand that it was necessary to give me the means of getting there.
"


Henri stated that he believes de Gaulle never forgave him for refusing to join the Free French in London, and also noted that "De Gaulle was not my friend...De Gaulle and I shared some common ideals and I agreed with him on the essentials of his approach to politics...
"


In 1988, Henri produced a scandal among his monarchist supporters when he supported the re-election of François Mitterrand, a socialist.
Political beliefs

In his college years, Henri spent many nights listening to the French monarchist writer Charles Maurras.
But during his adult life, Henri considered himself a centrist and never allied with any political party.
On Action Française, Henri stated that it had many talented leaders, but he ultimately regarded it as "a Rightist party with extreme Right sympathies."
In Henri's view, "no one should be in a position to claim a monopoly on the monarchist idea.
"


Henri befriended politicians on both the left and right, and declined to run for Parliament, despite de Gaulle's suggestion that he should do so.
Some rightist critics of Henri regarded him as "the Crown Prince of the Republic" or "a dyed-in-the-wool socialist, if not a Jacobin."
"


Henri was a critic of primogeniture and favored elective monarchy over hereditary.
Marriage and family life

On 8 April 1931, he married Princess Isabelle of Orléans-Braganza.
The wedding was celebrated in Palermo Cathedral in Sicily, the same church where their common ancestors, Louis Philippe of France and his Queen Maria Amalia, married in 1809.
In 1984, Henri declared that his son, Henri of Orléans, had lost his rights of inheritance because he had divorced his first wife and married a second time, outside of the Roman Catholic Church.
Henri gave his son the lesser-valued title comte de Mortain in place of comte de Clermont, and removed him from the line of succession.
After a couple of years, Henri reinstated his son with his previous titles, including reestablishing him as heir apparent and gave his new wife, Micaela Cousiño Quinones de Leon, the title "princesse de Joinville".
Henri deprived his sons Thibaut and Michel of their rights of succession to the defunct throne, because one married a commoner and the other wed a noblewoman whose father had been compromised during the Vichy regime.
His decision was later annulled by his son and successor, Henri.
Death

Henri, Count of Paris, died of prostate cancer at Cherisy, near Dreux, France, aged 90 on 19 June 1999.
Incidentally, his grandson Prince Eudes, Duke of Angoulême married on the very same day.
Issue

Henri, Count of Paris, and his wife Isabelle had eleven children:


Ancestry

References

Further reading

External links



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
  AssignClass (c4fdf444-4ce5-45ea-a25c-2d116e2e4646)
 Call ID: c4fdf444-4ce5-45ea-a25c-2d116e2e4646
  Args:
    source: Henri_dOrleans
    type: :Man
  AssignClass (119ac2c4-b8c5-409d-b2a2-896165586470)
 Call ID: 119ac2c4-b8c5-409d-b2a2-896165586470
  Args:
    source: Henri_dOrleans
    type: :Person
  AddLiteral (41e8213f-7a78-478c-89d6-af456f0b9822)
 Call ID: 41e8213f-7a78-478c-89d6-af456f0b9822
  Args:
    source: Henri_dOrleans
    literal_value: 1908
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bf9512ed-a881-41c4-b042-7b158e29a603)
 Call ID: bf9512ed-a881-41c4-b042-7b158e29a603
  Args:
    source: Henri_dOrleans
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1999
  AssignClass (9f868006-5a86-44e1-ad74-37a2af321000)
 Call ID: 9f868006-5a86-44e1-ad74-37a2af321000
  Args:
    type: :Man
    source: Jean_Duke_of_Guise
  AssignClass (39db0699-f5ca-461e-9ffa-86604be55e3f)
 Call ID: 39db0699-f5ca-461e-9ffa-86604be55e3f
  Args:
    source: Jean_Duke_of_Guise
    type: :Person
  AddTriple (71eabe4b-e184-468c-845a-9c9151317029)
 Call ID: 71eabe4b-e184-468c-845a-9c9151317029
  Args:
    target: Henri_dOrleans
    source: Jean_Duke_of_Guise
    relation: :isFatherOf
  AssignClass (fc35156c-7a03-4bab-89ba-6129bcf298fa)
 Call ID: fc35156c-7a03-4bab-89ba-6129bcf298fa
  Args:
    type: :Woman
    source: Isabelle_of_Orleans_Braganza
  AssignClass (0ca21647-8e9b-4ebf-a762-8f98b32c91d7)
 Call ID: 0ca21647-8e9b-4ebf-a762-8f98b32c91d7
  Args:
    type: :Person
    source: Isabelle_of_Orleans_Braganza
  AddTriple (4273e487-5067-41b3-9fcb-b965416eb8e5)
 Call ID: 4273e487-5067-41b3-9fcb-b965416eb8e5
  Args:
    target: Isabelle_of_Orleans_Braganza
    source: Henri_dOrleans
    relation: :hasRelation
  AddLiteral (0d49fe85-a295-4cc0-baed-6b54f1263eb3)
 Call ID: 0d49fe85-a295-4cc0-baed-6b54f1263eb3
  Args:
    source: Henri_dOrleans
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1931
  AssignClass (83f8a81a-9570-481a-a567-8140409771b3)
 Call ID: 83f8a81a-9570-481a-a567-8140409771b3
  Args:
    source: Henri_of_Orleans_son
    type: :Man
  AssignClass (1f2e360a-dbbb-4527-9e40-051ac8abc678)
 Call ID: 1f2e360a-dbbb-4527-9e40-051ac8abc678
  Args:
    type: :Person
    source: Henri_of_Orleans_son
  AddTriple (033dbae9-6bec-4423-9df3-a93c36920252)
 Call ID: 033dbae9-6bec-4423-9df3-a93c36920252
  Args:
    relation: :isFatherOf
    source: Henri_dOrleans
    target: Henri_of_Orleans_son
  AssignClass (9c3780fd-27b8-43d7-8f94-f203009fbb63)
 Call ID: 9c3780fd-27b8-43d7-8f94-f203009fbb63
  Args:
    source: Thibaut
    type: :Man
  AssignClass (2ef3d198-8e26-40b9-acaf-ac91d7e357c3)
 Call ID: 2ef3d198-8e26-40b9-acaf-ac91d7e357c3
  Args:
    type: :Person
    source: Thibaut
  AddTriple (203edeb8-d3ae-490f-9ae1-4d7e001ca2e3)
 Call ID: 203edeb8-d3ae-490f-9ae1-4d7e001ca2e3
  Args:
    source: Henri_dOrleans
    target: Thibaut
    relation: :isFatherOf
  AssignClass (5086733f-f1ca-42c1-9d10-069ff2ee0bc3)
 Call ID: 5086733f-f1ca-42c1-9d10-069ff2ee0bc3
  Args:
    type: :Man
    source: Michel
  AssignClass (6da44e75-6e89-4089-8c3f-6190b6703510)
 Call ID: 6da44e75-6e89-4089-8c3f-6190b6703510
  Args:
    type: :Person
    source: Michel
  AddTriple (5e900cf0-41d3-4ece-8615-4758ce8cc251)
 Call ID: 5e900cf0-41d3-4ece-8615-4758ce8cc251
  Args:
    source: Henri_dOrleans
    target: Michel
    relation: :isFatherOf
  AssignClass (76dc72fb-7c5c-4893-9646-b778e7665564)
 Call ID: 76dc72fb-7c5c-4893-9646-b778e7665564
  Args:
    type: :Man
    source: Eudes_Duke_of_Angouleme
  AssignClass (19f65955-815c-4015-bf06-c716ce2d1b2b)
 Call ID: 19f65955-815c-4015-bf06-c716ce2d1b2b
  Args:
    type: :Person
    source: Eudes_Duke_of_Angouleme
  AddTriple (95f33ce1-2a49-40bd-842f-67578188d49e)
 Call ID: 95f33ce1-2a49-40bd-842f-67578188d49e
  Args:
    relation: :isFatherOf
    target: Eudes_Duke_of_Angouleme
    source: Henri_of_Orleans_son
  AssignClass (b552ffad-1850-49e2-bc37-453df08ea1ed)
 Call ID: b552ffad-1850-49e2-bc37-453df08ea1ed
  Args:
    source: Philippe_I_Duke_of_Orleans
    type: :Man
  AssignClass (d4be2571-8dc2-49fb-9a36-9418b969609e)
 Call ID: d4be2571-8dc2-49fb-9a36-9418b969609e
  Args:
    source: Philippe_I_Duke_of_Orleans
    type: :Ancestor
  AssignClass (75252a71-ba99-459d-9795-13b1be9f4f70)
 Call ID: 75252a71-ba99-459d-9795-13b1be9f4f70
  Args:
    source: Louis_XIII
    type: :Man
  AssignClass (53b4e73a-4a98-4b8d-a25a-7f08126d5519)
 Call ID: 53b4e73a-4a98-4b8d-a25a-7f08126d5519
  Args:
    type: :Ancestor
    source: Louis_XIII
  AddTriple (6598d5c1-32c7-4d0b-a3ce-9d53b9d2b922)
 Call ID: 6598d5c1-32c7-4d0b-a3ce-9d53b9d2b922
  Args:
    target: Philippe_I_Duke_of_Orleans
    source: Louis_XIII
    relation: :isFatherOf
  AddTriple (98bd38e2-c73c-49be-b7a9-569cb4e3204f)
 Call ID: 98bd38e2-c73c-49be-b7a9-569cb4e3204f
  Args:
    relation: :hasAncestor
    target: Philippe_I_Duke_of_Orleans
    source: Henri_dOrleans
  AssignClass (eab49de7-9797-4e84-99d7-f4aa51d1bd92)
 Call ID: eab49de7-9797-4e84-99d7-f4aa51d1bd92
  Args:
    source: Louis_XIV
    type: :Man
  AssignClass (29a1c61f-e9ef-4c14-b54e-282824aebb7e)
 Call ID: 29a1c61f-e9ef-4c14-b54e-282824aebb7e
  Args:
    source: Louis_XIV
    type: :Ancestor
  AssignClass (baea3b1a-c9e3-4e7e-b6bc-a62ab11477d6)
 Call ID: baea3b1a-c9e3-4e7e-b6bc-a62ab11477d6
  Args:
    source: Francoise_Marie_de_Bourbon
    type: :Woman
  AssignClass (1f47b058-2382-46b4-80e4-f0211bf6cb06)
 Call ID: 1f47b058-2382-46b4-80e4-f0211bf6cb06
  Args:
    source: Francoise_Marie_de_Bourbon
    type: :Ancestor
  AddTriple (44492b3e-1f1c-4f0a-9b90-b7cbcef1c6c2)
 Call ID: 44492b3e-1f1c-4f0a-9b90-b7cbcef1c6c2
  Args:
    target: Francoise_Marie_de_Bourbon
    source: Louis_XIV
    relation: :isFatherOf
  AddTriple (2ac4e221-2de6-4733-a444-c337bd344065)
 Call ID: 2ac4e221-2de6-4733-a444-c337bd344065
  Args:
    relation: :hasAncestor
    target: Francoise_Marie_de_Bourbon
    source: Henri_dOrleans
  AssignClass (3221fc8a-1830-4bbb-95fd-fe143a018eda)
 Call ID: 3221fc8a-1830-4bbb-95fd-fe143a018eda
  Args:
    type: :Man
    source: Louis_Philippe_I
  AssignClass (81c097de-fa15-4a02-ac52-6a315fb658c9)
 Call ID: 81c097de-fa15-4a02-ac52-6a315fb658c9
  Args:
    source: Louis_Philippe_I
    type: :Ancestor
  AddTriple (7de264c9-cae1-439b-b558-a99ec64c66a1)
 Call ID: 7de264c9-cae1-439b-b558-a99ec64c66a1
  Args:
    target: Louis_Philippe_I
    source: Henri_dOrleans
    relation: :hasAncestor
  Finish (c5abd613-225d-42f1-8705-44b8e8ccd2af)
 Call ID: c5abd613-225d-42f1-8705-44b8e8ccd2af
  Args: